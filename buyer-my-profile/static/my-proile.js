
  function editCoverImage() {
    const fileInput = document.getElementById('coverImageInput');
    fileInput.click();
  }

  function handleFileSelect(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    if (file && file.type.startsWith('image/')) {
      // Set the selected image as the new cover image
      const coverImage = document.getElementById('coverImage');
      coverImage.src = URL.createObjectURL(file);
    } else {
      alert('Please select a valid image file.');
      // Reset the file input
      fileInput.value = '';
    }
  }

  function editProfileImage() {
    const fileInput = document.getElementById('profileImageInput');
    fileInput.click();
  }

  function handleProfileImageSelect(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    if (file && file.type.startsWith('image/')) {
      // Set the selected image as the new profile image
      const profileImage = document.getElementById('profileImage');
      profileImage.src = URL.createObjectURL(file);
    } else {
      alert('Please select a valid image file.');
      // Reset the file input
      fileInput.value = '';
    }
  }
