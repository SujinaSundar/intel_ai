import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

interface MainLayoutProps {

    children: React.ReactNode;

}

export default function MainLayout({

    children,

}: MainLayoutProps) {

    return (

        <div className="flex min-h-screen bg-background text-foreground">

            {/* ------------------------------------------ */}
            {/* Sidebar */}
            {/* ------------------------------------------ */}

            <Sidebar />

            {/* ------------------------------------------ */}
            {/* Main Content */}
            {/* ------------------------------------------ */}

            <div className="flex min-w-0 flex-1 flex-col">

                {/* -------------------------------------- */}
                {/* Navigation */}
                {/* -------------------------------------- */}

                <Navbar />

                {/* -------------------------------------- */}
                {/* Page Content */}
                {/* -------------------------------------- */}

                <main className="flex-1 overflow-y-auto">

                    <div
                        className="
                            mx-auto
                            w-full
                            max-w-7xl
                            px-6
                            py-8
                            sm:px-8
                            lg:px-10
                            xl:px-12
                        "
                    >

                        {children}

                    </div>

                </main>

            </div>

        </div>

    );

}