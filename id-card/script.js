  const nicknameInput = document.getElementById('nickname');
  const dobInput = document.getElementById('dob');
  const addressInput = document.getElementById('address');
  const sfInput = document.getElementById('sf');
  const womanRadio = document.getElementById('woman');
  const manRadio = document.getElementById('man');
  const photoInput = document.getElementById('photo-upload');
  const signatureCanvas = document.getElementById('sig-pad');
  const saveButton = document.getElementById('save-card');
  const signatureDiv = document.getElementById('p-signature');
  const form = document.querySelector('form');
  const header = document.querySelector('header');
  const body = document.querySelector('body');

  const pName = document.getElementById('p-name');
  const pSex = document.getElementById('p-sex');
  const pDob = document.getElementById('p-dob');
  const pAddress = document.getElementById('p-legal-address');
  const pSf = document.getElementById('p-special-features');

  const deletePhotoButton = document.getElementById('delete-photo');
  const clearSignatureButton = document.getElementById('clear-signature');
  const resetButton = document.getElementById('reset');
  const saveCardButton = document.getElementById('save-card');

  const signaturePad = new SignaturePad(signatureCanvas);
  
  function updateButtonsState() {
    const isFormFilled = nicknameInput.value.trim() !== '' ||
                         dobInput.value.trim() !== '' ||
                         addressInput.value.trim() !== '' ||
                         sfInput.value.trim() !== '' ||
                         womanRadio.checked ||
                         manRadio.checked;
    
    const isPhotoLoaded = photoInput.files.length > 0;
    const isSignatureDrawn = !signaturePad.isEmpty();
    
    const canClearOrDelete = isPhotoLoaded || isSignatureDrawn;
    const canReset = isFormFilled || canClearOrDelete;
    
    deletePhotoButton.disabled = !isPhotoLoaded;
    clearSignatureButton.disabled = !isSignatureDrawn;
    resetButton.disabled = !canReset;
    saveCardButton.disabled = !(isFormFilled && isPhotoLoaded && isSignatureDrawn);
  }

  function validateForm() {
    const emptyFields = [];
    if (nicknameInput.value.trim() === '') emptyFields.push(nicknameInput);
    if (dobInput.value.trim() === '') emptyFields.push(dobInput);
    if (addressInput.value.trim() === '') emptyFields.push(addressInput);
    if (sfInput.value.trim() === '') emptyFields.push(sfInput);
    const isSexSelected = womanRadio.checked || manRadio.checked;
    if (!isSexSelected) emptyFields.push(womanRadio); 
    if (photoInput.files.length === 0) emptyFields.push(photoInput);
    if (signaturePad.isEmpty()) emptyFields.push(signatureCanvas);
    return true;
  }
  
  function updateSignature() {
    if (!signaturePad.isEmpty()) {
      const dataURL = signaturePad.toDataURL();
      signatureDiv.innerHTML = `<img src="${dataURL}" style="width:100%; height:auto; object-fit:contain;">`;
    }
    updateButtonsState(); 
  }

  saveButton.addEventListener('click', () => {
    if (validateForm()) {
      html2canvas(document.getElementById('card')).then(canvas => {
        const link = document.createElement('a');
        link.download = 'krospilets_card.png';
        link.href = canvas.toDataURL();
        link.click();
      });
    }
  });

  document.getElementById('clear-signature').addEventListener('click', () => {
    signaturePad.clear();
    signatureDiv.innerHTML = '';
    updateButtonsState();
  });

  document.getElementById('delete-photo').addEventListener('click', () => {
    document.getElementById('p-photo').style.backgroundImage = 'none';
    document.getElementById('photo-upload').value = '';
    updateButtonsState();
  });

  signatureCanvas.addEventListener('mouseup', updateSignature);
  signatureCanvas.addEventListener('touchend', updateSignature);
  signatureCanvas.addEventListener('mousemove', updateSignature);
  signatureCanvas.addEventListener('touchmove', updateSignature);
  
  nicknameInput.addEventListener('input', (e) => {
    document.getElementById('p-name').textContent = e.target.value;
    updateButtonsState();
  });
  dobInput.addEventListener('change', (e) => {
    const date = new Date(e.target.value);
    const formattedDate = date.toLocaleDateString('uk-UA', { day: '2-digit', month: '2-digit', year: 'numeric' });
    document.getElementById('p-dob').textContent = formattedDate;
    updateButtonsState();
  });
  addressInput.addEventListener('input', (e) => {
    document.getElementById('p-legal-address').textContent = e.target.value;
    updateButtonsState();
  });
  sfInput.addEventListener('input', (e) => {
    document.getElementById('p-special-features').textContent = e.target.value;
    updateButtonsState();
  });

  womanRadio.addEventListener('change', () => {
    document.getElementById('p-sex').textContent = 'Жіноча';
    updateButtonsState();
  });
  manRadio.addEventListener('change', () => {
    document.getElementById('p-sex').textContent = 'Чоловіча';
    updateButtonsState();
  });

  photoInput.addEventListener('change', e => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        document.getElementById('p-photo').style.backgroundImage = `url(${reader.result})`;
      };
      reader.readAsDataURL(file);
    }
    updateButtonsState();
  });
  
  resetButton.addEventListener('click', () => {
    pName.textContent = '';
    pSex.textContent = '';
    pDob.textContent = '';
    pAddress.textContent = '';
    pSf.textContent = '';
    signaturePad.clear();
    signatureDiv.innerHTML = '';
    document.getElementById('p-photo').style.backgroundImage = 'none';
    document.getElementById('photo-upload').value = '';
    
    setTimeout(updateButtonsState, 0); 
  });

  document.getElementById('p-date-of-issue').textContent = new Date().toLocaleDateString('uk-UA');
  let expireDate = new Date();
  expireDate.setFullYear(expireDate.getFullYear() + 10);
  document.getElementById('p-date-of-expire').textContent = expireDate.toLocaleDateString('uk-UA');
  document.getElementById('p-record').textContent = Math.floor(Math.random() * 9999999);

  function updateBodyPadding() {
    const headerHeight = header.offsetHeight;
    body.style.paddingTop = `${headerHeight + 20}px`;
  }

  window.addEventListener('load', () => {
    updateBodyPadding();
    updateButtonsState();
  });
  window.addEventListener('resize', updateBodyPadding);