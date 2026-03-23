import { useState } from 'react';
import CourseList, { Course } from './components/CourseList';
import SelectedCourses from './components/SelectedCourses';
import styles from './App.module.css';

// 샘플 과목 데이터
const MOCK_COURSES: Course[] = [
  {
    id: '1',
    name: '자료구조',
    code: 'CS201',
    professor: '김철수',
    credits: 3,
    time: '월/수 10:30-12:00',
    capacity: 40,
    enrolled: 35,
  },
  {
    id: '2',
    name: '알고리즘',
    code: 'CS301',
    professor: '이영희',
    credits: 3,
    time: '화/목 13:00-14:30',
    capacity: 35,
    enrolled: 30,
  },
  {
    id: '3',
    name: '데이터베이스',
    code: 'CS302',
    professor: '박민수',
    credits: 3,
    time: '월/수 14:00-15:30',
    capacity: 45,
    enrolled: 45,
  },
  {
    id: '4',
    name: '운영체제',
    code: 'CS303',
    professor: '정수진',
    credits: 3,
    time: '화/목 09:00-10:30',
    capacity: 40,
    enrolled: 28,
  },
  {
    id: '5',
    name: '컴퓨터네트워크',
    code: 'CS304',
    professor: '최준호',
    credits: 3,
    time: '월/수 16:00-17:30',
    capacity: 35,
    enrolled: 20,
  },
  {
    id: '6',
    name: '소프트웨어공학',
    code: 'CS305',
    professor: '강지훈',
    credits: 3,
    time: '화/목 15:00-16:30',
    capacity: 30,
    enrolled: 25,
  },
];

export default function App() {
  const [selectedCourses, setSelectedCourses] = useState<Course[]>([]);

  const handleAddCourse = (course: Course) => {
    if (!selectedCourses.find((c) => c.id === course.id)) {
      setSelectedCourses([...selectedCourses, course]);
    }
  };

  const handleRemoveCourse = (courseId: string) => {
    setSelectedCourses(selectedCourses.filter((c) => c.id !== courseId));
  };

  const selectedCourseIds = selectedCourses.map((c) => c.id);

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>수강신청</h1>
        <p className={styles.subtitle}>원하는 과목을 선택하세요</p>
      </header>

      <div className={styles.content}>
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>개설 과목</h2>
          <CourseList
            courses={MOCK_COURSES}
            selectedCourseIds={selectedCourseIds}
            onAddCourse={handleAddCourse}
          />
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>내 수강 목록</h2>
          <SelectedCourses
            courses={selectedCourses}
            onRemoveCourse={handleRemoveCourse}
          />
        </section>
      </div>
    </div>
  );
}
