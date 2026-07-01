"use client";
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  CheckSquare, 
  Activity, 
  Users, 
  Settings, 
  Briefcase, 
  Database,
  KanbanSquare
} from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Tasks', href: '/tasks', icon: CheckSquare, badge: 2 },
    { name: 'Activity', href: '/activity', icon: Activity },
    { name: 'Datasets', href: '/datasets', icon: Database },
    { name: 'Jobs', href: '/jobs', icon: KanbanSquare },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  const projects = [
    { name: 'BizConnect', badge: 7 },
    { name: 'Growth Hub' },
    { name: 'Conversion Path' },
    { name: 'Marketing' },
  ];

  const members = [
    { name: 'Sandra Perry', role: 'Product Manager', initial: 'SP', color: 'bg-blue-500' },
    { name: 'Antony Cardenas', role: 'Sales Manager', initial: 'AC', color: 'bg-green-500' },
    { name: 'Jamal Connolly', role: 'Growth Marketer', initial: 'JC', color: 'bg-orange-500' },
    { name: 'Cara Carr', role: 'SEO Specialist', initial: 'CC', color: 'bg-purple-500' },
  ];

  return (
    <aside className="w-64 border-r border-border bg-card/50 flex flex-col h-screen sticky top-0">
      <div className="h-16 flex items-center px-6">
        <Link href="/" className="flex items-center space-x-2 font-bold text-xl tracking-tight">
          <Briefcase className="h-5 w-5 text-emerald-400" />
          <span>FeatureLab AI</span>
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-8">
        {/* Main Navigation */}
        <nav className="space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.name === 'Datasets' && pathname.startsWith('/datasets'));
            return (
              <Link 
                key={item.name} 
                href={item.href}
                className={`flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive 
                    ? 'bg-accent text-accent-foreground' 
                    : 'text-muted-foreground hover:bg-accent/50 hover:text-foreground'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <item.icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span className="bg-primary/10 text-primary text-xs font-semibold px-2 py-0.5 rounded-full">
                    {item.badge}
                  </span>
                )}
              </Link>
            )
          })}
        </nav>
      </div>

      <div className="p-4 border-t border-border/50">
        <div className="flex items-center space-x-3 cursor-pointer">
          <Avatar className="h-9 w-9">
            <AvatarFallback className="bg-emerald-600 text-white">AD</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <p className="text-sm font-medium leading-none mb-1">Admin User</p>
            <p className="text-xs text-muted-foreground leading-none">Admin</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
