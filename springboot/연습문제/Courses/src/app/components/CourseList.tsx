import styles from './CourseList.module.css';

export interface Course {
  id: string;
  name: string;
  code: string;
  professor: string;
  credits: number;
  time: string;
  capacity: number;
  enrolled: number;
}

interface CourseListProps {
  courses: Course[];
  selectedCourseIds: string[];
  onAddCourse: (course: Course) => void;
}

export default function CourseList({ courses, selectedCourseIds, onAddCourse }: CourseListProps) {
  return (
    <div>
      {courses.map((course) => {
        const isSelected = selectedCourseIds.includes(course.id);
        const isFull = course.enrolled >= course.capacity;

        return (
          <div key={course.id} className={styles.courseItem}>
            <div className={styles.courseHeader}>
              <div className={styles.courseInfo}>
                <h3 className={styles.courseName}>{course.name}</h3>
                <p className={styles.courseCode}>{course.code}</p>
                <div className={styles.courseDetails}>
                  <span className={styles.courseDetail}>👤 {course.professor}</span>
                  <span className={styles.courseDetail}>📚 {course.credits}학점</span>
                  <span className={styles.courseDetail}>🕐 {course.time}</span>
                  <span className={styles.courseDetail}>
                    👥 {course.enrolled}/{course.capacity}
                  </span>
                </div>
              </div>
              <button
                className={styles.addButton}
                onClick={() => onAddCourse(course)}
                disabled={isSelected || isFull}
              >
                {isSelected ? '신청됨' : isFull ? '마감' : '신청'}
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
