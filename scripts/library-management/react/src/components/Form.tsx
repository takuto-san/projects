export default function Form({ onSubmit, children }: { onSubmit: (e: React.SubmitEvent<HTMLFormElement>) => void; children: React.ReactNode }) {
    return (
        <form onSubmit={onSubmit}>
            {children}
        </form>
    );
}