"use client";

import { useState, useCallback } from "react";
import { Movie } from "@/app/api/movies/route";
import MovieCard from "@/components/MovieCard";
import LoadingSkeleton from "@/components/LoadingSkeleton";

interface ApiResponse {
  movies: Movie[];
  scrapedAt: string;
  error?: string;
  detail?: string;
}

export default function Home() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [scrapedAt, setScrapedAt] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const fetchMovies = useCallback(async () => {
    setLoading(true);
    setError("");
    setMovies([]);

    try {
      const res = await fetch("/api/movies");
      const data: ApiResponse = await res.json();

      if (!res.ok || data.error) {
        throw new Error(data.detail || data.error || "알 수 없는 오류");
      }

      setMovies(data.movies);
      setScrapedAt(data.scrapedAt);
    } catch (err) {
      setError(err instanceof Error ? err.message : "오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  }, []);

  const formattedTime = scrapedAt
    ? new Date(scrapedAt).toLocaleString("ko-KR", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      })
    : "";

  return (
    <main className="min-h-screen bg-gray-950">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-gray-950/90 backdrop-blur-md border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-red-600 flex items-center justify-center text-white font-black text-sm">
              M
            </div>
            <div>
              <h1 className="text-lg font-bold text-white leading-tight">
                메가박스 박스오피스
              </h1>
              <p className="text-xs text-gray-400">실시간 TOP 10</p>
            </div>
          </div>
          {formattedTime && (
            <p className="text-xs text-gray-500 hidden sm:block">
              업데이트: {formattedTime}
            </p>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 pt-16 pb-12 text-center">
        <h2 className="text-4xl sm:text-5xl font-black mb-4 bg-gradient-to-r from-red-500 via-orange-400 to-yellow-400 bg-clip-text text-transparent">
          박스오피스 TOP 10
        </h2>
        <p className="text-gray-400 mb-10 text-base sm:text-lg">
          메가박스 홈페이지에서 실시간 예매율 순위를 가져옵니다
        </p>

        <button
          onClick={fetchMovies}
          disabled={loading}
          className="group relative inline-flex items-center gap-2 px-8 py-4 rounded-2xl font-bold text-lg bg-red-600 hover:bg-red-500 disabled:bg-gray-700 disabled:text-gray-500 transition-all duration-200 shadow-lg shadow-red-900/30 hover:shadow-red-800/50 hover:scale-105 active:scale-95 disabled:scale-100 disabled:shadow-none"
        >
          {loading ? (
            <>
              <span className="inline-block w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              스크래핑 중...
            </>
          ) : (
            <>
              <svg
                className="w-5 h-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              {movies.length > 0 ? "새로고침" : "순위 불러오기"}
            </>
          )}
        </button>

        {loading && (
          <p className="mt-4 text-sm text-gray-500 animate-pulse">
            메가박스 페이지를 렌더링하는 중... (약 20~30초 소요)
          </p>
        )}
      </section>

      {/* Error Message */}
      {error && (
        <div className="max-w-2xl mx-auto px-4 mb-8">
          <div className="bg-red-950/50 border border-red-800 rounded-2xl p-5 text-center">
            <div className="text-red-400 text-2xl mb-2">⚠️</div>
            <p className="text-red-300 font-medium">스크래핑 오류</p>
            <p className="text-red-400/80 text-sm mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Loading Skeletons */}
      {loading && (
        <div className="max-w-7xl mx-auto px-4 pb-16">
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {Array.from({ length: 10 }).map((_, i) => (
              <LoadingSkeleton key={i} />
            ))}
          </div>
        </div>
      )}

      {/* Movie Grid */}
      {!loading && movies.length > 0 && (
        <div className="max-w-7xl mx-auto px-4 pb-16">
          {/* Top 3 큰 카드 */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-5">
            {movies.slice(0, 3).map((movie) => (
              <MovieCard key={movie.rank} movie={movie} featured />
            ))}
          </div>
          {/* 4~10위 작은 카드 */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-4">
            {movies.slice(3).map((movie) => (
              <MovieCard key={movie.rank} movie={movie} />
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && movies.length === 0 && (
        <div className="text-center pb-24 text-gray-600">
          <div className="text-6xl mb-4">🎬</div>
          <p className="text-lg">버튼을 눌러 순위를 불러오세요</p>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-gray-900 py-6 text-center text-xs text-gray-600">
        메가박스 (megabox.co.kr) 데이터를 Puppeteer로 스크래핑합니다
      </footer>
    </main>
  );
}
