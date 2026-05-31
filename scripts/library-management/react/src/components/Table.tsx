export default function Table({ books = [] }: { books?: string[] }) {
    return (
        <table border={1}>
            <thead>
                <tr>
                    <th>no.</th>
                    <th>ID</th>
                </tr>
            </thead>
            <tbody>
                {[...Array(10)].map((_, i) => (
                    <tr key={i}>
                        <td>{i + 1}</td>
                        <td>{books[i] || ""}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}