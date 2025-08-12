   function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('-translate-x-full');
  }








   function toggleSidebar() {
      const sidebar = document.getElementById('sidebar');
      sidebar.classList.toggle('-translate-x-full');
    }

    function deleteRow(btn) {
      if (confirm('Are you sure you want to delete this submission?')) {
        const row = btn.closest('tr');
        row.remove();
        // TODO: Integrate with backend (AJAX or Django view) for actual delete
      }
    }



const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');

imageInput.addEventListener('change', () => {
  previewContainer.innerHTML = ''; // Clear previous previews

  const files = imageInput.files;
  if (files.length === 0) {
    return;
  }

  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = document.createElement('img');
      img.src = e.target.result;
      img.classList.add('h-24', 'w-24', 'object-contain', 'border', 'p-1', 'rounded');
      previewContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});




  let currentEditRow = null;

  function openEditModal(row) {
    currentEditRow = row;
    const categoryName = row.querySelector('.category-name').innerText;
    document.getElementById('editCategoryName').value = categoryName;
    document.getElementById('editModal').classList.remove('hidden');
  }

  function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
  }

  document.getElementById('editForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const updatedName = document.getElementById('editCategoryName').value;
    if (currentEditRow) {
      currentEditRow.querySelector('.category-name').innerText = updatedName;
    }
    closeEditModal();
  });
