import io
import pandas as pd
import joblib
from uuid import UUID
from domain.entities import Experiment, Artifact
from services.storage import StorageService
from ml_engine.orchestrator import TaskDetector, PipelineBuilder
from ml_engine.pipelines.preprocessing import PreprocessingPipeline
from ml_engine.pipelines.feature_engineering import FeatureEngineeringPipeline
from ml_engine.pipelines.feature_selection import FeatureSelectionPipeline
from ml_engine.pipelines.model_benchmark import ModelBenchmarkPipeline

async def ml_pipeline_task(
    job_id: UUID,
    dataset_id: UUID,
    workspace_id: UUID,
    target_column: str,
    user_config: dict,
    db_session
):
    from api.deps import get_dataset_repo, get_experiment_repo, get_artifact_repo
    from repositories.sql_repositories import DatasetRepository, ExperimentRepository, ArtifactRepository
    
    dataset_repo = DatasetRepository(db_session)
    experiment_repo = ExperimentRepository(db_session)
    artifact_repo = ArtifactRepository(db_session)
    storage = StorageService()
    
    # 1. Fetch Dataset
    dataset = dataset_repo.get_by_id(dataset_id)
    if not dataset:
        raise ValueError(f"Dataset {dataset_id} not found")
        
    # 2. Download CSV
    csv_bytes = storage.download_file(dataset.file_path)
    df = pd.read_csv(io.BytesIO(csv_bytes))
    
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not in dataset")
        
    y = df[target_column]
    X = df.drop(columns=[target_column])
    
    # 3. Detect Task and Build Config
    task_type = TaskDetector.detect_task(dataset.profile_data, target_column)
    config = PipelineBuilder.build_config(task_type, user_config)
    
    # 4. Create Experiment
    import uuid
    from datetime import datetime
    experiment_id = uuid.uuid4()
    experiment = Experiment(
        id=experiment_id,
        workspace_id=workspace_id,
        dataset_id=dataset_id,
        name=f"Experiment for {dataset.name}",
        task_type=task_type,
        target_column=target_column,
        configuration=config,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    experiment_repo.create(experiment)
    
    # 5. Preprocessing
    preprocessor = PreprocessingPipeline(config)
    preprocessor.fit(X, y)
    X_prep = preprocessor.transform(X)
    
    # 6. Feature Engineering
    fe_pipeline = FeatureEngineeringPipeline(config)
    fe_pipeline.fit(X_prep, y)
    X_fe = fe_pipeline.transform(X_prep)
    
    # 7. Feature Selection
    fs_pipeline = FeatureSelectionPipeline(config, task_type)
    fs_pipeline.fit(X_fe, y)
    X_fs = fs_pipeline.transform(X_fe)
    
    # 8. Model Benchmarking
    benchmark = ModelBenchmarkPipeline(config, task_type)
    metrics = benchmark.fit_and_evaluate(X_fs, y)
    
    best_model_name = list(metrics.keys())[0] if metrics else None
    
    # SHAP Explainability
    shap_results = {}
    if best_model_name:
        from ml_engine.pipelines.explainability import ExplainabilityPipeline
        explainer = ExplainabilityPipeline(benchmark.trained_models[best_model_name], task_type)
        shap_results = explainer.explain(X_fs)
    
    # 9. Update Experiment Metrics
    experiment.metrics = {
        "benchmark": metrics,
        "shap": shap_results
    }
    
    # 10. Save Artifacts
    # Saving preprocessor
    prep_buffer = io.BytesIO()
    joblib.dump(preprocessor, prep_buffer)
    prep_path = f"{workspace_id}/artifacts/{experiment_id}_preprocessor.joblib"
    storage.upload_file(prep_path, prep_buffer.getvalue())
    artifact_repo.create(Artifact(
        id=uuid.uuid4(), workspace_id=workspace_id, experiment_id=experiment_id,
        name="Preprocessor Pipeline", artifact_type="pipeline", file_path=prep_path,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow()
    ))
    
    if best_model_name:
        model_buffer = io.BytesIO()
        joblib.dump(benchmark.trained_models[best_model_name], model_buffer)
        model_path = f"{workspace_id}/artifacts/{experiment_id}_model.joblib"
        storage.upload_file(model_path, model_buffer.getvalue())
        artifact_repo.create(Artifact(
            id=uuid.uuid4(), workspace_id=workspace_id, experiment_id=experiment_id,
            name=f"Best Model ({best_model_name})", artifact_type="model", file_path=model_path,
            created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        ))
        
    return "SUCCESS"
