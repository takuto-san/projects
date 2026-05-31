export const registerBooks = async (userId: string, books: string[]) => {
    const endpoint = `http://localhost:8080/users/${userId}/borrowing`;

    const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bookIds: books })
  });

  if (!response.ok) {
    throw new Error('Faileds to register books');
  }

  return await response.json();
};