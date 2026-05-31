import { useLocation, Link } from 'react-router-dom';

export default function Completed() {
  const { state } = useLocation();
  const borrowings = state?.borrowings || [];

  return (
    <div>
      <h1>登録完了</h1>
      <ul>
        {borrowings.map((b: any) => (
          <li key={b.id}>
            {b.item.book.title} （アイテムID: {b.item.id}）
          </li>
        ))}
      </ul>
      
      <Link to="/dashboard">戻る</Link>
    </div>
  );
}