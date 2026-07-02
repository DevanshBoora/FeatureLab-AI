"use client";
import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { datasetApi, DEFAULT_WORKSPACE_ID } from '@/lib/api';

export default function DatasetUpload({ onUploadSuccess }: { onUploadSuccess: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      if (!name) setName(acceptedFiles[0].name.split('.')[0]);
    }
  }, [name]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    maxFiles: 1
  });

  const handleUpload = async () => {
    if (!file || !name) return;
    
    setUploading(true);
    setError(null);
    try {
      await datasetApi.upload(DEFAULT_WORKSPACE_ID, name, file, description);
      setFile(null);
      setName('');
      setDescription('');
      onUploadSuccess();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.response?.data?.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4 p-4 border rounded-lg bg-card text-card-foreground">
      <h3 className="text-lg font-medium">Upload Dataset</h3>
      
      {!file ? (
        <div {...getRootProps()} className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-10 text-center cursor-pointer hover:bg-muted/50 transition-colors">
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>Drop the CSV file here ...</p>
          ) : (
            <p>Drag & drop a CSV file here, or click to select one</p>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3 border rounded">
            <span className="truncate max-w-[300px]">{file.name}</span>
            <Button variant="ghost" size="sm" onClick={() => setFile(null)}>Remove</Button>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="name">Dataset Name</Label>
            <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Dataset Name" />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="description">Description (Optional)</Label>
            <Input id="description" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="What is this dataset about?" />
          </div>
          
          {error && <p className="text-destructive text-sm">{error}</p>}
          
          <Button onClick={handleUpload} disabled={uploading || !name} className="w-full">
            {uploading ? "Uploading & Profiling..." : "Upload & Profile Dataset"}
          </Button>
        </div>
      )}
    </div>
  );
}
