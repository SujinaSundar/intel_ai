"use client";

/**
 * Navbar.
 *
 * Top navigation bar for
 * the Intel AI Trading
 * Research Platform.
 */

import { Activity, Sparkles, LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

import { logout } from "@/services/auth.service";

export default function Navbar() {
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.replace("/login");
  };

  return (
    <header
      className="
        sticky
        top-0
        z-40
        border-b
        border-border
        bg-background/90
        backdrop-blur-xl
      "
    >
      <div
        className="
          mx-auto
          flex
          h-20
          max-w-7xl
          items-center
          justify-between
          px-6
          sm:px-8
          lg:px-10
          xl:px-12
        "
      >
        {/* Brand */}

        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <div
              className="
                flex
                h-9
                w-9
                items-center
                justify-center
                rounded-xl
                bg-primary/10
                text-primary
              "
            >
              <Sparkles className="h-5 w-5" />
            </div>

            <h2 className="text-2xl font-bold tracking-tight">
              Intel AI
            </h2>
          </div>

          <p className="mt-1 text-sm text-muted-foreground">
            Multi-Agent Trading Research Platform
          </p>
        </div>

        {/* Right Section */}

        <div className="flex items-center gap-4">
          {/* Status */}

          <div
            className="
              flex
              items-center
              gap-3
              rounded-full
              border
              border-border
              bg-card
              px-4
              py-2
              shadow-sm
            "
          >
            <span className="relative flex h-3 w-3">
              <span
                className="
                  absolute
                  inline-flex
                  h-full
                  w-full
                  animate-ping
                  rounded-full
                  bg-green-500
                  opacity-40
                "
              />

              <span
                className="
                  relative
                  inline-flex
                  h-3
                  w-3
                  rounded-full
                  bg-green-500
                "
              />
            </span>

            <Activity className="h-4 w-4 text-green-500" />

            <div className="flex flex-col leading-none">
              <span className="text-sm font-semibold">
                System Online
              </span>

              <span className="text-xs text-muted-foreground">
                All services operational
              </span>
            </div>
          </div>

          {/* Logout Button */}

          <button
            onClick={handleLogout}
            className="
              flex
              items-center
              gap-2
              rounded-lg
              border
              border-red-300
              px-4
              py-2
              text-sm
              font-medium
              text-red-600
              transition
              hover:bg-red-50
            "
          >
            <LogOut className="h-4 w-4" />
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}