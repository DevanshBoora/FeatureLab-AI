"use client";
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import DatasetUpload from '@/components/DatasetUpload';
import { datasetApi, DEFAULT_WORKSPACE_ID } from '@/lib/api';
import Link from 'next/link';

export default function DatasetsPage() {
  const [datasets, setDatasets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const data = await datasetApi.list(DEFAULT_WORKSPACE_ID);
      setDatasets(data);
    } catch (error) {
      console.error("Failed to fetch datasets", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  return (
    <div className="p-8 pt-8 space-y-8">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Datasets</h2>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-4">
        <Card className="col-span-4 bg-card/40 border-border">
          <CardHeader>
            <CardTitle>All Datasets</CardTitle>
            <CardDescription>Manage your uploaded datasets here.</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Rows</TableHead>
                  <TableHead>Columns</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow><TableCell colSpan={4} className="text-center">Loading...</TableCell></TableRow>
                ) : datasets.length === 0 ? (
                  <TableRow><TableCell colSpan={4} className="text-center">No datasets found.</TableCell></TableRow>
                ) : (
                  datasets.map((dataset) => (
                    <TableRow key={dataset.id}>
                      <TableCell className="font-medium">{dataset.name}</TableCell>
                      <TableCell>{dataset.row_count?.toLocaleString() || '-'}</TableCell>
                      <TableCell>{dataset.column_count || '-'}</TableCell>
                      <TableCell>
                        <Link href={`/datasets/${dataset.id}`}>
                          <Button variant="outline" size="sm" className="bg-zinc-800 border-zinc-700 text-zinc-100 hover:bg-zinc-700">View Details</Button>
                        </Link>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
        
        <div className="col-span-3">
          <DatasetUpload onUploadSuccess={fetchDatasets} />
        </div>
      </div>
    </div>
  );
}
