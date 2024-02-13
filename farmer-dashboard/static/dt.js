// Add this script to the end of your existing JavaScript

// Sample inventory data (you can replace this with your backend data)
let inventory = [
  { id: 1, name: 'Item 1', quantity: 10 },
  { id: 2, name: 'Item 2', quantity: 5 },
];

// Function to render inventory table
function renderInventory() {
  const tableBody = document.getElementById('inventoryTableBody');
  tableBody.innerHTML = '';

  inventory.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.name}</td>
      <td>${item.quantity}</td>
      <td>
        <button class="btn btn-info btn-sm" onclick="editItem(${item.id})">Edit</button>
        <button class="btn btn-danger btn-sm" onclick="deleteItem(${item.id})">Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

// Function to add a new item
function addItem() {
  const itemName = prompt('Enter item name:');
  if (itemName) {
    const newItem = { id: inventory.length + 1, name: itemName, quantity: 0 };
    inventory.push(newItem);
    renderInventory();
  }
}

// Function to edit an existing item
function editItem(itemId) {
  const item = inventory.find(item => item.id === itemId);
  const newQuantity = prompt(`Enter new quantity for ${item.name}:`, item.quantity);
  if (newQuantity !== null && !isNaN(newQuantity)) {
    item.quantity = parseInt(newQuantity, 10);
    renderInventory();
  }
}

// Function to delete an item
function deleteItem(itemId) {
  const confirmDelete = confirm('Are you sure you want to delete this item?');
  if (confirmDelete) {
    inventory = inventory.filter(item => item.id !== itemId);
    renderInventory();
  }
}

// Initial render
renderInventory();
