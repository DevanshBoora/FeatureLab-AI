import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex-col md:flex">
      <div className="flex-1 space-y-4 p-8 pt-6">
        <div className="flex items-center justify-between space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">FeatureLab AI</h2>
        </div>
        <div className="flex flex-col items-center justify-center space-y-4 text-center mt-20">
          <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl max-w-4xl bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
            Automate Your Machine Learning Pipelines
          </h1>
          <p className="max-w-2xl text-lg text-muted-foreground mt-4">
            Upload your datasets, profile data instantly, engineer features automatically, 
            and evaluate models with our enterprise-grade AI orchestrator.
          </p>
          <div className="flex space-x-4 mt-8">
            <Link href="/dashboard">
              <Button size="lg" className="h-12 px-8 text-base font-semibold">
                Go to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
