
<script>
  let cropper;

  function openImageCropModal() {
    // Reset the file input and Cropper instance
    const cropImageInput = document.getElementById('cropImageInput');
    cropImageInput.value = '';
    cropper = null;

    // Show the modal
    const imageCropModal = new bootstrap.Modal(document.getElementById('imageCropModal'));
    imageCropModal.show();
  }

  function loadImageForCropping() {
    // Get the file input and selected file
    const cropImageInput = document.getElementById('cropImageInput');
    const file = cropImageInput.files[0];

    if (file && file.type.startsWith('image/')) {
      // Set the source of the cropper image
      const cropperImage = document.getElementById('cropperImage');
      cropperImage.src = URL.createObjectURL(file);

      // Initialize Cropper.js with profile image crop ratio
      cropper = new Cropper(cropperImage, {
        aspectRatio: 1, // Set the aspect ratio for the profile image
        viewMode: 1, // Set the view mode
      });
    } else {
      alert('Please select a valid image file.');
    }
  }

  function saveCroppedImage() {
    if (cropper) {
      // Get the cropped data
      const croppedData = cropper.getData();

      // Perform any additional actions with the cropped data (e.g., save to server)

      // Update the profile image on the profile
      const profileImage = document.getElementById('profileImage');
      profileImage.src = cropper.getCroppedCanvas().toDataURL();

      // Close the modal after a delay
      const imageCropModal = new bootstrap.Modal(document.getElementById('imageCropModal'));
      setTimeout(() => {
        imageCropModal.hide();
      }, 3000); // 3000 milliseconds (3 seconds) delay
    } else {
      alert('No image loaded for cropping.');
    }
  }
</script>


<!-- Modal for Image Cropping -->
<div class="modal fade" id="imageCropModal" tabindex="-1" aria-labelledby="imageCropModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="imageCropModalLabel">Crop Profile Image</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <input type="file" id="cropImageInput" accept="image/*">
        <button class="btn btn-primary" onclick="loadImageForCropping()">Load Image</button>
        <hr>
        <div class="text-center">
          <img id="cropperImage" src="" alt="Croppable Image" style="max-width: 100%;" class="img-fluid">
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-primary" onclick="saveCroppedImage()">Save</button>
      </div>
    </div>
  </div>
</div>

