import { NextResponse } from "next/server";
import puppeteer from "puppeteer";

export interface Movie {
  rank: number;
  title: string;
  bookingRate: string;
  releaseDate: string;
  rating: string;
  ratingClass: string;
  poster: string;
  dDay: string;
  score: string;
  movieNo: string;
}

export async function GET() {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
      ],
    });

    const page = await browser.newPage();

    await page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    );

    await page.setViewport({ width: 1280, height: 900 });

    await page.goto("https://www.megabox.co.kr/movie", {
      waitUntil: "networkidle2",
      timeout: 30000,
    });

    // 영화 목록이 렌더링될 때까지 대기
    await page.waitForSelector(".movie-list-wrap, .movie-wrap, ol.list", {
      timeout: 15000,
    });

    // 추가 렌더링 대기
    await new Promise((res) => setTimeout(res, 2000));

    const movies = await page.evaluate(() => {
      const results: {
        rank: number;
        title: string;
        bookingRate: string;
        releaseDate: string;
        rating: string;
        ratingClass: string;
        poster: string;
        dDay: string;
        score: string;
        movieNo: string;
      }[] = [];

      const items = document.querySelectorAll("ol.list > li");
      if (!items || items.length === 0) return results;

      Array.from(items)
        .slice(0, 10)
        .forEach((item) => {
          // 순위
          const rankEl = item.querySelector(".rank");
          const rankText = rankEl?.childNodes[0]?.textContent?.trim() || "";
          const rank = parseInt(rankText, 10) || 0;

          // 제목
          const titleEl = item.querySelector(".tit-area .tit");
          const title = titleEl?.textContent?.trim() || titleEl?.getAttribute("title") || "";

          // 포스터 (lozad 레이지로딩 - src 또는 data-src)
          const imgEl = item.querySelector("img.poster");
          const poster =
            imgEl?.getAttribute("src") ||
            imgEl?.getAttribute("data-src") ||
            "";

          // 예매율 (예: "예매율 21.8%")
          const rateEl = item.querySelector(".rate-date .rate");
          const bookingRate = rateEl?.textContent?.trim().replace("예매율", "").trim() || "";

          // 개봉일 (예: "개봉일 2026.03.18")
          const dateEl = item.querySelector(".rate-date .date");
          const releaseDate = dateEl?.textContent?.trim().replace("개봉일", "").trim() || "";

          // 관람등급 (클래스에서 판별: age-all, age-12, age-15, age-18, age-19)
          const gradeEl = item.querySelector(".movie-grade");
          const ratingClass = gradeEl?.className || "";
          let rating = "전체";
          if (ratingClass.includes("age-12")) rating = "12세";
          else if (ratingClass.includes("age-15")) rating = "15세";
          else if (ratingClass.includes("age-18") || ratingClass.includes("age-19")) rating = "청불";
          else if (ratingClass.includes("age-all")) rating = "전체";

          // 메가박스 관람평
          const scoreEl = item.querySelector(".my-score .number");
          const score = scoreEl?.childNodes[0]?.textContent?.trim() || "";

          // D-Day 상태 표시
          const dDayEl = item.querySelector(".txt.movieStat1");
          const dDayHtmlEl = dDayEl as HTMLElement | null;
          const dDay =
            dDayHtmlEl?.style?.display !== "none"
              ? dDayHtmlEl?.textContent?.trim() || ""
              : "";

          // 영화 번호 (상세 링크용)
          const linkEl = item.querySelector("a.movieBtn");
          const movieNo = linkEl?.getAttribute("data-no") || "";

          if (title) {
            results.push({
              rank,
              title,
              bookingRate,
              releaseDate,
              rating,
              ratingClass,
              poster,
              dDay,
              score,
              movieNo,
            });
          }
        });

      return results;
    });

    await browser.close();

    if (movies.length === 0) {
      return NextResponse.json(
        { error: "영화 데이터를 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다." },
        { status: 404 }
      );
    }

    return NextResponse.json({ movies, scrapedAt: new Date().toISOString() });
  } catch (error) {
    if (browser) await browser.close();
    console.error("Scraping error:", error);
    return NextResponse.json(
      {
        error: "스크래핑 중 오류가 발생했습니다.",
        detail: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}
