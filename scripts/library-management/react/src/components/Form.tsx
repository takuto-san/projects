export default function Form({ onSubmit, children }: { onSubmit: () => void; children: React.ReactNode }) {
    return (
        <form onSubmit={onSubmit}>
            {children}
        </form>
    );
}