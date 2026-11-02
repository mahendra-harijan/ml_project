import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Briefcase, LayoutDashboard, FileText } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? "bg-indigo-700 text-white" : "text-indigo-100 hover:bg-indigo-600 hover:text-white";
  };

  return (
    <nav className="bg-indigo-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center space-x-2 text-white">
              <Briefcase className="h-8 w-8" />
              <span className="font-bold text-xl tracking-tight">AI Recruiter</span>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link to="/" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/')}`}>
                  <div className="flex items-center space-x-1">
                    <LayoutDashboard className="h-4 w-4" />
                    <span>Dashboard</span>
                  </div>
                </Link>
                <Link to="/screening" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/screening')}`}>
                  <div className="flex items-center space-x-1">
                    <FileText className="h-4 w-4" />
                    <span>Screening</span>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
