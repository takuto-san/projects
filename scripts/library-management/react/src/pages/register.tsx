import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Table from '../components/Table';
import Form from '../components/Form';
import { registerItems } from '../api/booksApi';

export default function Register() {
  const navigate = useNavigate();

  const [input, setInput] = useState('');
  const [items, setItems] = useState<string[]>([]);
  const userId = "test@example.com";

  const handleScan = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!input) return;

    setItems((prev) => [...prev, input]);
    setInput('');
  };

  const handleSendItems = async () => {
    if (items.length === 0) return alert("No items to register");

    try {
      const result = await registerItems(userId, items);
      navigate('/completed', { state: { borrowings: result } });
    } catch (error) {
      alert("Failed to register items");
      console.error(error);
    }
  }

  return (
    <div>
      <h1>図書マスター</h1>
      <Button text="戻る" size="small" type="button" onClick={() => navigate('/dashboard')} />
      <br />
      <Table items={items} />
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
        onClick={handleSendItems} 
      />
    </div>
  );
}