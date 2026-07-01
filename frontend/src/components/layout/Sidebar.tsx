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

        {/* Projects Section */}
        <div>
          <h4 className="px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
            Projects
          </h4>
          <nav className="space-y-1">
            {projects.map((project) => (
              <div key={project.name} className="flex items-center justify-between px-3 py-2 rounded-md text-sm text-muted-foreground hover:bg-accent/30 cursor-pointer transition-colors">
                <div className="flex items-center space-x-3">
                  <div className="h-2 w-2 rounded-full bg-emerald-400/70" />
                  <span>{project.name}</span>
                </div>
                {project.badge && (
                  <span className="bg-muted text-muted-foreground text-xs font-medium px-2 py-0.5 rounded-full">
                    {project.badge}
                  </span>
                )}
              </div>
            ))}
          </nav>
        </div>

        {/* Members Section */}
        <div>
          <div className="flex items-center justify-between px-4 mb-3">
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Members
            </h4>
            <button className="text-muted-foreground hover:text-foreground">+</button>
          </div>
          <div className="space-y-3 px-3">
            {members.map((member) => (
              <div key={member.name} className="flex items-center space-x-3 cursor-pointer group">
                <Avatar className="h-8 w-8">
                  <AvatarFallback className={`text-xs text-white ${member.color}`}>{member.initial}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="text-sm font-medium text-foreground group-hover:text-emerald-400 transition-colors leading-none mb-1">{member.name}</p>
                  <p className="text-[10px] text-muted-foreground leading-none">{member.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="p-4 border-t border-border/50">
        <div className="flex items-center space-x-3 cursor-pointer">
          <Avatar className="h-9 w-9">
            <AvatarImage src="https://github.com/shadcn.png" />
            <AvatarFallback>IO</AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <p className="text-sm font-medium leading-none mb-1">Iona Rollins</p>
            <p className="text-xs text-muted-foreground leading-none">Admin</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
