document.querySelectorAll('.group-card').forEach(card => {
    card.addEventListener('click', function(e) {
        // Avoid triggering expand when clicking the edit button
        if(e.target.classList.contains('edit-btn')) return;

        const details = card.querySelector('.group-details');
        if(details.style.display === 'block'){
            details.style.display = 'none';
        } else {
            details.style.display = 'block';
        }
    });
});

function editGroup(groupId){
    // Redirect to edit page (you can create a /groups/<id>/edit route)
    window.location.href = `/create?group_id=${groupId}`;
}

function deleteGroup(groupId){
    if (confirm("Are you sure you want to delete this group?")) {
        fetch(`/groups/${groupId}`, {
            method: "DELETE"
        })
        .then(res => {
            if (res.ok) {
                window.location.reload();
            } else {
                alert("Failed to delete group.");
            }
        });
    }
}