import { Course } from './CourseList';
import styles from './SelectedCourses.module.css';

interface SelectedCoursesProps {
  courses: Course[];
  onRemoveCourse: (courseId: string) => void;
}

export default function SelectedCourses({ courses, onRemoveCourse }: SelectedCoursesProps) {
  const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);

  if (courses.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p>선택한 과목이 없습니다</p>
      </div>
    );
  }

  return (
    <div>
      {courses.map((course) => (
        <div key={course.id} className={styles.selectedItem}>
          <div className={styles.itemHeader}>
            <div>
              <h4 className={styles.itemName}>{course.name}</h4>
              <p className={styles.itemCode}>{course.code}</p>
            </div>
            <button
              className={styles.removeButton}
              onClick={() => onRemoveCourse(course.id)}
              title="삭제"
            >
              ×
            </button>
          </div>
          <div className={styles.itemDetails}>
            <div>{course.professor} 교수</div>
            <div>{course.time} · {course.credits}학점</div>
          </div>
        </div>
      ))}

      <div className={styles.summary}>
        <div className={styles.summaryItem}>
          <span>선택 과목 수</span>
          <span>{courses.length}개</span>
        </div>
        <div className={styles.summaryTotal}>
          <span>총 학점</span>
          <span>{totalCredits}학점</span>
        </div>
      </div>
    </div>
  );
}
