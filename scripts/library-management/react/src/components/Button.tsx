export default function Button({ text, size, type, onClick }: { text: string; size: 'large' | 'small'; type: 'button' | 'submit'; onClick?: () => void }) {
  const padding = size === 'large' ? '16px 32px' : '4px 8px';
  const fontSize = size === 'large' ? '20px' : '12px';

  return (
    <button onClick={onClick} style={{ padding, fontSize, margin: '4px' }} type={type}>
      {text}
    </button>
  );
}