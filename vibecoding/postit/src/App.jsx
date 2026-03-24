import { useState, useEffect, useRef } from 'react';
import { supabase } from './supabase.js';
import styles from './app.module.css';

const NOTE_COLORS = [
  { bg: '#fff9c4', header: '#fff176' },
  { bg: '#fce4ec', header: '#f48fb1' },
  { bg: '#e8f5e9', header: '#a5d6a7' },
  { bg: '#e3f2fd', header: '#90caf9' },
  { bg: '#ede7f6', header: '#ce93d8' },
  { bg: '#fff3e0', header: '#ffcc80' },
];

function Note({ note, onDelete, onChange }) {
  const color = NOTE_COLORS[note.color_idx];
  const timer = useRef(null);

  function handleChange(field, value) {
    onChange(note.id, field, value);
    clearTimeout(timer.current);
    timer.current = setTimeout(async () => {
      const { error } = await supabase.from('notes').update({ [field]: value }).eq('id', note.id);
      if (error) console.error('update error:', error);
    }, 600);
  }

  return (
    <div className={styles.card} style={{ background: color.bg }}>
      <div className={styles.cardHeader} style={{ background: color.header }}>
        <button className={styles.deleteBtn} onClick={() => onDelete(note.id)}>✕</button>
      </div>
      <div className={styles.cardBody}>
        <input
          className={styles.titleInput}
          placeholder="제목"
          value={note.title}
          onChange={(e) => handleChange('title', e.target.value)}
        />
        <textarea
          className={styles.contentTextarea}
          placeholder="내용을 입력하세요..."
          value={note.content}
          onChange={(e) => handleChange('content', e.target.value)}
        />
      </div>
    </div>
  );
}

export default function App() {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    supabase
      .from('notes')
      .select('*')
      .order('created_at', { ascending: true })
      .then(({ data, error }) => {
        if (error) setError(error.message);
        else setNotes(data || []);
        setLoading(false);
      });
  }, []);

  async function addNote() {
    const newNote = {
      title: '',
      content: '',
      color_idx: Math.floor(Math.random() * NOTE_COLORS.length),
    };
    const { data, error } = await supabase.from('notes').insert(newNote).select().single();
    if (!error) setNotes((prev) => [...prev, data]);
  }

  async function deleteNote(id) {
    const { error } = await supabase.from('notes').delete().eq('id', id);
    if (!error) setNotes((prev) => prev.filter((n) => n.id !== id));
  }

  function changeNote(id, field, value) {
    setNotes((prev) => prev.map((n) => n.id === id ? { ...n, [field]: value } : n));
  }

  if (loading) {
    return (
      <div className={styles.app}>
        <p className={styles.empty}>불러오는 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.app}>
        <p className={styles.empty}>오류: {error}</p>
      </div>
    );
  }

  return (
    <div className={styles.app}>
      <div className={styles.header}>
        <h1 className={styles.title}>📌 포스트잇</h1>
        <button className={styles.addBtn} onClick={addNote}>＋ 추가</button>
      </div>
      <div className={styles.board}>
        {notes.length === 0
          ? <p className={styles.empty}>+ 버튼을 눌러 포스트잇을 추가해보세요!</p>
          : notes.map((note) => (
              <Note
                key={note.id}
                note={note}
                onDelete={deleteNote}
                onChange={changeNote}
              />
            ))
        }
      </div>
    </div>
  );
}
