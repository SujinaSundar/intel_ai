"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import MainLayout from "@/components/layout/MainLayout";
import { validateToken } from "@/services/auth.service";

interface ProtectedLayoutProps {
  children: React.ReactNode;
}

export default function ProtectedLayout({
  children,
}: ProtectedLayoutProps) {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    async function checkAuth() {
      const valid = await validateToken();

      if (!valid) {
        router.replace("/login");
        return;
      }

      setAuthenticated(true);
      setLoading(false);
    }

    checkAuth();
  }, [router]);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        Checking authentication...
      </div>
    );
  }

  if (!authenticated) {
    return null;
  }

  return <MainLayout>{children}</MainLayout>;
}