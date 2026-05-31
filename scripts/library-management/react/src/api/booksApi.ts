export const registerItems = async (userId: string, items: string[]) => {
    const endpoint = `http://localhost:8080/users/${userId}/borrowings`;

    const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item_ids: items })
  });

  if (!response.ok) {
    throw new Error('Faileds to register items');
  }

  return await response.json();
};