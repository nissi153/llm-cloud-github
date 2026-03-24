"use client";

import Image from "next/image";
import { Movie } from "@/app/api/movies/route";

const RANK_GRADIENT = [
  "from-yellow-400 to-orange-500",
  "from-slate-300 to-slate-400",
  "from-orange-400 to-amber-600",
];

const RATING_COLOR: Record<string, string> = {
  전체: "bg-green-600",
  "12세": "bg-yellow-500",
  "15세": "bg-orange-500",
  청불: "bg-red-600",
};

interface MovieCardProps {
  movie: Movie;
  featured?: boolean;
}

export default function MovieCard({ movie, featured = false }: MovieCardProps) {
  const isTop3 = movie.rank <= 3;
  const gradientClass = isTop3 ? RANK_GRADIENT[movie.rank - 1] : null;
  const ratingColor = RATING_COLOR[movie.rating] ?? "bg-gray-600";
  const detailUrl = movie.movieNo
    ? `https://www.megabox.co.kr/movie/detail?movieNo=${movie.movieNo}`
    : "https://www.megabox.co.kr/movie";

  return (
    <a
      href={detailUrl}
      target="_blank"
      rel="noopener noreferrer"
      className={`
        group block relative rounded-2xl overflow-hidden bg-gray-900 transition-all duration-300
        hover:scale-[1.03] hover:shadow-2xl hover:shadow-black/70
        ${isTop3 ? "ring-1 ring-white/10" : "ring-1 ring-gray-800 hover:ring-gray-600"}
      `}
    >
      {/* Poster */}
      <div className="relative w-full aspect-[2/3] overflow-hidden">
        {movie.poster ? (
          <Image
            src={movie.poster}
            alt={movie.title}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-105"
            unoptimized
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gray-800 text-gray-500 text-xs text-center px-3 leading-relaxed">
            {movie.title}
          </div>
        )}

        {/* Dark gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/10 to-transparent" />

        {/* Rank badge */}
        <div className="absolute top-2.5 left-2.5">
          <span
            className={`
              inline-flex items-center justify-center rounded-xl font-black shadow-lg
              ${featured ? "w-10 h-10 text-xl" : "w-7 h-7 text-sm"}
              ${
                isTop3
                  ? `bg-gradient-to-br ${gradientClass} text-gray-900`
                  : "bg-black/70 text-gray-300 backdrop-blur-sm"
              }
            `}
          >
            {movie.rank}
          </span>
        </div>

        {/* Booking rate */}
        {movie.bookingRate && (
          <div className="absolute top-2.5 right-2.5">
            <span className="bg-red-600/90 backdrop-blur-sm text-white text-xs font-bold px-2 py-1 rounded-lg">
              {movie.bookingRate}
            </span>
          </div>
        )}

        {/* D-Day */}
        {movie.dDay && (
          <div className="absolute bottom-14 right-2.5">
            <span className="bg-indigo-600/90 backdrop-blur-sm text-white text-xs font-semibold px-2 py-1 rounded-lg">
              {movie.dDay}
            </span>
          </div>
        )}

        {/* Score */}
        {movie.score && movie.score !== "0" && (
          <div className="absolute bottom-14 left-2.5">
            <span className="flex items-center gap-1 bg-black/70 backdrop-blur-sm text-yellow-400 text-xs font-bold px-2 py-1 rounded-lg">
              ★ {movie.score}
            </span>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-3 space-y-1.5">
        <h3
          className={`font-bold text-white leading-snug line-clamp-2 ${
            featured ? "text-[15px]" : "text-[13px]"
          }`}
        >
          {movie.title}
        </h3>

        <div className="flex items-center gap-1.5 flex-wrap">
          <span
            className={`text-[10px] font-bold text-white px-1.5 py-0.5 rounded ${ratingColor}`}
          >
            {movie.rating}
          </span>
          {movie.releaseDate && (
            <span className="text-[11px] text-gray-500">{movie.releaseDate}</span>
          )}
        </div>
      </div>
    </a>
  );
}
