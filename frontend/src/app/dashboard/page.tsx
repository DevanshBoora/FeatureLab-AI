"use client";
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { jobApi, datasetApi, DEFAULT_WORKSPACE_ID } from '@/lib/api';
import { MoreVertical, Calendar, MessageSquare, ArrowRight } from 'lucide-react';
import { Progress } from "@/components/ui/progress";

export default function DashboardPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [datasets, setDatasets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [fetchedJobs, fetchedDatasets] = await Promise.all([
        jobApi.list(DEFAULT_WORKSPACE_ID).catch(() => []),
        datasetApi.list(DEFAULT_WORKSPACE_ID).catch(() => [])
      ]);
      setJobs(fetchedJobs);
      setDatasets(fetchedDatasets);
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getDatasetName = (datasetId: string) => {
    const ds = datasets.find(d => d.id === datasetId);
    return ds ? ds.name : 'Unknown Dataset';
  };

  const columns = [
    { title: 'Queued', statuses: ['QUEUED'] },
    { title: 'Running', statuses: ['RUNNING'] },
    { title: 'Completed', statuses: ['COMPLETED'] },
    { title: 'Failed', statuses: ['FAILED'] }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'QUEUED': return 'bg-zinc-500';
      case 'RUNNING': return 'bg-blue-500';
      case 'COMPLETED': return 'bg-emerald-500';
      case 'FAILED': return 'bg-red-500';
      default: return 'bg-zinc-500';
    }
  };

  const calculateSuccessRate = () => {
    if (jobs.length === 0) return 0;
    const completed = jobs.filter(j => j.status === 'COMPLETED').length;
    return Math.round((completed / jobs.length) * 100);
  };

  return (
    <div className="p-8 pt-8 space-y-8">
      {/* Top Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 bg-card/40 rounded-xl p-6 border border-border">
        {/* Total Datasets */}
        <div className="space-y-4 flex flex-col justify-center">
          <div>
            <h3 className="text-sm font-medium text-muted-foreground mb-1">Total Datasets</h3>
            <div className="flex items-end gap-2">
              <span className="text-4xl font-bold tracking-tight">{datasets.length}</span>
              <span className="text-sm text-muted-foreground mb-1">processed</span>
            </div>
          </div>
          
          <div className="flex h-[80px] items-end gap-2">
            {[4, 6, 8, 5, 9].map((h, i) => (
              <div key={i} className="w-8 bg-zinc-800 rounded-sm" style={{ height: `${h * 10}%` }}>
                <div className="w-full bg-emerald-400/80 rounded-sm" style={{ height: `${(h - 2) * 10}%` }} />
              </div>
            ))}
          </div>
        </div>

        {/* Circular Progress (Success Rate) */}
        <div className="flex flex-col items-center justify-center border-x border-border/50">
          <div className="relative flex items-center justify-center w-36 h-36">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-muted/20"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeDasharray="100, 100"
              />
              <path
                className="text-emerald-400"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeDasharray={`${calculateSuccessRate()}, 100`}
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center">
              <span className="text-2xl font-bold">{calculateSuccessRate()}%</span>
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest mt-1">Success</span>
            </div>
          </div>
        </div>

        {/* Right Stats */}
        <div className="flex flex-col justify-center space-y-6 pl-4">
          <div>
            <span className="text-4xl font-bold tracking-tight">{jobs.length}</span>
            <div className="text-sm text-muted-foreground flex items-center justify-between mt-1">
              <span>Total Jobs</span>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
            </div>
          </div>
          <div className="h-px bg-border/50 w-full" />
          <div>
            <span className="text-2xl font-bold tracking-tight text-emerald-400">{jobs.filter(j => j.status === 'RUNNING').length}</span>
            <div className="text-sm text-muted-foreground flex items-center justify-between mt-1">
              <span>Jobs running</span>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
            </div>
          </div>
        </div>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 overflow-x-auto pb-4">
        {columns.map(col => {
          const colJobs = jobs.filter(j => col.statuses.includes(j.status));
          
          return (
            <div key={col.title} className="flex flex-col min-w-[280px]">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-foreground/90">{col.title}</h3>
                <span className="text-xs font-medium px-2 py-1 bg-accent text-muted-foreground rounded-md">
                  {colJobs.length} ↑↓
                </span>
              </div>
              
              <div className="space-y-4">
                {colJobs.map(job => (
                  <Card key={job.id} className={`border-border shadow-sm hover:border-emerald-400/50 transition-colors ${job.status === 'RUNNING' ? 'bg-zinc-900/50' : 'bg-card'}`}>
                    <CardHeader className="p-4 pb-2">
                      <div className="flex items-start justify-between">
                        <div className="space-y-1">
                          <CardTitle className="text-sm font-semibold leading-none">
                            {getDatasetName(job.dataset_id)}
                          </CardTitle>
                          <CardDescription className="text-xs mt-2 line-clamp-2">
                            Automated ML pipeline for target column {job.configuration?.target_column || 'unknown'}.
                          </CardDescription>
                        </div>
                        <button className="text-muted-foreground hover:text-foreground">
                          <MoreVertical className="h-4 w-4" />
                        </button>
                      </div>
                    </CardHeader>
                    {job.status === 'RUNNING' && (
                      <div className="px-4 py-2">
                        <Progress value={job.progress * 100} className="h-1.5" />
                        <span className="text-[10px] text-emerald-400 mt-1 block">{(job.progress * 100).toFixed(0)}% Complete</span>
                      </div>
                    )}
                    <CardFooter className="p-4 pt-2 flex items-center justify-between border-t border-border/40 mt-2">
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <Calendar className="h-3 w-3" />
                        <span>{new Date(job.created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' })}</span>
                      </div>
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <MessageSquare className="h-3 w-3" />
                        <span>{Object.keys(job.configuration || {}).length}</span>
                      </div>
                    </CardFooter>
                  </Card>
                ))}
                
                {colJobs.length === 0 && (
                  <div className="border-2 border-dashed border-border/50 rounded-lg h-24 flex items-center justify-center text-sm text-muted-foreground">
                    No jobs
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
