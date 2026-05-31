export default function Button({ text, size, onClick }: { text: string; size: 'large' | 'small'; onClick?: () => void }) {
  const padding = size === 'large' ? '16px 32px' : '4px 8px';
  const fontSize = size === 'large' ? '20px' : '12px';

  return (
    <button onClick={onClick} style={{ padding, fontSize, margin: '4px' }}>
      {text}
    </button>
  );
}