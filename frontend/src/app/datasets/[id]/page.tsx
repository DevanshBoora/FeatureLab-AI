"use client";
import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { datasetApi, jobApi, DEFAULT_WORKSPACE_ID } from '@/lib/api';

export default function DatasetDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [dataset, setDataset] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [targetColumn, setTargetColumn] = useState<string>("");
  const [startingJob, setStartingJob] = useState(false);

  useEffect(() => {
    if (id) {
      datasetApi.get(id as string).then(data => {
        setDataset(data);
        setLoading(false);
      }).catch(err => {
        console.error(err);
        setLoading(false);
      });
    }
  }, [id]);

  const handleStartExperiment = async () => {
    if (!targetColumn) return;
    setStartingJob(true);
    try {
      const job = await jobApi.submit(DEFAULT_WORKSPACE_ID, dataset.id, "training", {
        target_column: targetColumn,
        imputation: "median",
        encoding: "onehot",
        scaling: "standard"
      });
      router.push(`/experiments`); // ideally redirect to the job/experiment page
    } catch (err) {
      console.error(err);
    } finally {
      setStartingJob(false);
    }
  };

  if (loading) return <div className="p-8">Loading dataset...</div>;
  if (!dataset) return <div className="p-8">Dataset not found.</div>;

  const columns = dataset.profile_data?.columns || {};
  const columnNames = Object.keys(columns);

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">{dataset.name}</h2>
        <Badge variant="outline">{(dataset.file_size_bytes / 1024).toFixed(2)} KB</Badge>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Rows</CardTitle>
          </CardHeader>
          <CardContent><div className="text-2xl font-bold">{dataset.row_count}</div></CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Columns</CardTitle>
          </CardHeader>
          <CardContent><div className="text-2xl font-bold">{dataset.column_count}</div></CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Duplicates</CardTitle>
          </CardHeader>
          <CardContent><div className="text-2xl font-bold">{dataset.profile_data?.duplicate_percentage.toFixed(2)}%</div></CardContent>
        </Card>
      </div>

      <div className="mt-8 grid gap-4 md:grid-cols-3 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Column Profiling</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Column</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Missing %</TableHead>
                  <TableHead>Unique</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {columnNames.map(col => (
                  <TableRow key={col}>
                    <TableCell className="font-medium">{col}</TableCell>
                    <TableCell>{columns[col].type}</TableCell>
                    <TableCell>{columns[col].missing_percentage.toFixed(2)}%</TableCell>
                    <TableCell>{columns[col].unique_count}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Start Experiment</CardTitle>
            <CardDescription>Select a target column to start training models automatically.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Target Column</label>
              <Select onValueChange={(val) => setTargetColumn(val || "")} value={targetColumn}>
                <SelectTrigger>
                  <SelectValue placeholder="Select target..." />
                </SelectTrigger>
                <SelectContent>
                  {columnNames.map(col => (
                    <SelectItem key={col} value={col}>{col}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Button onClick={handleStartExperiment} disabled={!targetColumn || startingJob} className="w-full">
              {startingJob ? "Submitting..." : "Run AutoML Pipeline"}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
