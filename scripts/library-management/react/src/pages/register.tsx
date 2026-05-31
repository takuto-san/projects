import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Table from '../components/Table';
import Form from '../components/Form';

export default function Register() {
  const navigate = useNavigate();

  const [input, setInput] = useState('');
  const [books, setBooks] = useState<string[]>([]);

  const handleScan = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!input) return;

    setBooks((prev) => [...prev, input]);
    setInput('');
  };

  return (
    <div>
      <h1>図書マスター</h1>
      <Button text="戻る" size="small" type="button" onClick={() => navigate('/dashboard')} />
      <Table books={books} />
      <br/>
      <Form onSubmit={handleScan}>
        <input
          autoFocus
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <Button text="送信" size="small" type="submit" />
      </Form>
    </div>
  );
}