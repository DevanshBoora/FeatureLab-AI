"use client";
import React from 'react';
import { Search, SlidersHorizontal, User as UserIcon, Plus } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Header() {
  return (
    <header className="h-20 border-b border-border bg-background flex items-center justify-between px-8 sticky top-0 z-10">
      
      {/* Search Bar */}
      <div className="relative w-96">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-4 w-4 text-muted-foreground" />
        </div>
        <Input 
          type="text" 
          placeholder="Search jobs, datasets..." 
          className="pl-10 bg-accent/30 border-none h-10 focus-visible:ring-emerald-400/50 rounded-lg text-sm"
        />
      </div>

      {/* Right Actions */}
      <div className="flex items-center space-x-6">
        <button className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
          <SlidersHorizontal className="h-4 w-4" />
          <span>Sort by</span>
        </button>
        
        <button className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
          <SlidersHorizontal className="h-4 w-4" />
          <span>Filters</span>
        </button>

        <button className="flex items-center space-x-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
          <UserIcon className="h-4 w-4" />
          <span>Me</span>
        </button>

        <Button className="bg-zinc-800 hover:bg-zinc-700 text-zinc-100 rounded-lg px-4 shadow-sm border border-zinc-700">
          <Plus className="h-4 w-4 mr-2" />
          Add dataset
        </Button>
      </div>

    </header>
  );
}
