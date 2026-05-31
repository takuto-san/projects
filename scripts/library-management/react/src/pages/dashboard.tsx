import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>図書マスター</h1>            
      <Button text="貸出" size="large" type="button" onClick={() => navigate('/register')} />
      <Button text="返却" size="large" type="button" onClick={() => navigate('/register')} />
    </div>
  );
}