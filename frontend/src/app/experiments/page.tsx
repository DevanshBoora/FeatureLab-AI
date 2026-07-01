"use client";
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function ExperimentsPage() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Experiments</h2>
      </div>
      
      <div className="grid gap-4 mt-4">
        <Card>
          <CardHeader>
            <CardTitle>Recent Experiments</CardTitle>
            <CardDescription>Track your model training runs and benchmarks here.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center py-10 text-muted-foreground">
              Run an experiment from a dataset page to see results here.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
