import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();
  const [barcode, setBarcode] = useState('');

  return (
    <form onSubmit={(e) => { e.preventDefault(); navigate('/dashboard'); }}>
      <h2>会員証または社員証をかざしてください</h2>
      <input
        autoFocus // 画面を開いた瞬間に自動でカーソルを合わせる
        value={barcode}
        onChange={(e) => setBarcode(e.target.value)}
      />
    </form>
  );
}