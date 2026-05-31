import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Table from '../components/Table';
import Form from '../components/Form';
import { registerBooks } from '../api/booksApi';

export default function Register() {
  const navigate = useNavigate();

  const [input, setInput] = useState('');
  const [books, setBooks] = useState<string[]>([]);
  const userId = "test@example.com";

  const handleScan = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!input) return;

    setBooks((prev) => [...prev, input]);
    setInput('');
  };

  const handleSendBooks = async () => {
    if (books.length === 0) return alert("No books to register");

    try {
      await registerBooks(userId, books);
      navigate('/completed');
    } catch (error) {
      alert("Failed to register books");
      console.error(error);
    }
  }

  return (
    <div>
      <h1>図書マスター</h1>
      <Button text="戻る" size="small" type="button" onClick={() => navigate('/dashboard')} />
      <br />
      <Table books={books} />
      <br/>
      <Form onSubmit={handleScan}>
        <input
          autoFocus
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </Form>
      <br />
      <Button 
        text="送信" 
        size="small" 
        type="button" 
        onClick={handleSendBooks} 
      />
    </div>
  );
}