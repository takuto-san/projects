import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Table from '../components/Table';
import Form from '../components/Form';

export default function Register() {
  const navigate = useNavigate();

  const [input, setInput] = useState('');
  const [books, setBooks] = useState<string[]>([]);

  const handleScan = () => {

  };

  return (
    <div>
      <h1>図書マスター</h1>
      <Button text="戻る" size="small" onClick={() => navigate('/dashboard')} />
      <Table books={books} />
      <Form onSubmit={handleScan} />
        <Button />      
    </div>
  );
}