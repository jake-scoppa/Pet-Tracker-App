function deletePet(petId){
    fetch('/delete-pet',{
        method: 'POST',
        body: JSON.stringify({ petId: petId}),
    }).then((_res) =>{
        window.location.href = "/";
    });
}

document.getElementById('togglePetsSectionBtn').addEventListener('click', function () {
    var addPetsSection = document.getElementById('addPetsSection');
    addPetsSection.style.display = (addPetsSection.style.display === 'none' || addPetsSection.style.display === '') ? 'block' : 'none';
});