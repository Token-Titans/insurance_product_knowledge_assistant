import type { Metadata } from "next"
import { Geist_Mono, Noto_Sans_Myanmar, Nunito_Sans } from "next/font/google"

import "./globals.css"
import { I18nProvider } from "@/components/i18n-provider"
import { QueryProvider } from "@/components/query-provider"
import { ThemeProvider } from "@/components/theme-provider"
import { cn } from "@/lib/utils"

const nunitoSans = Nunito_Sans({ subsets: ["latin"], variable: "--font-sans" })

const myanmar = Noto_Sans_Myanmar({
  subsets: ["myanmar"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-myanmar",
})

const fontMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export const metadata: Metadata = {
  title: "InsureAssist",
  description: "Know the product. Answer with confidence.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="my"
      suppressHydrationWarning
      className={cn(
        "antialiased",
        "font-sans",
        nunitoSans.variable,
        myanmar.variable,
        fontMono.variable,
      )}
    >
      <body>
        <ThemeProvider>
          <I18nProvider>
            <QueryProvider>{children}</QueryProvider>
          </I18nProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
