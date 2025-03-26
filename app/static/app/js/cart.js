var updateBtns = document.getElementsByClassName('update-cart');

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, 'action', action)
        console.log('user: ', user)
        if (user === 'AnoymouseUser') {
            console.log('user not logged in')
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    var url = '/update_item/'
    console.log(csrftoken)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data', data)
            location.reload()
        })
}

var deleteBtn = document.getElementById('delete-selected');
var selectAllCheckbox = document.getElementById('select-all');
var itemCheckboxes = document.querySelectorAll('.item-checkbox');

// Khi thay đổi trạng thái của checkbox "Chọn tất cả"
selectAllCheckbox.addEventListener('change', function () {
    var isChecked = this.checked;
    itemCheckboxes.forEach(function (checkbox) {
        checkbox.checked = isChecked;
        updateUserOrder(checkbox.dataset.product, isChecked ? 'select' : 'unselect');
    });
});

// Kiểm tra trạng thái của tất cả các sản phẩm
itemCheckboxes.forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
        var productId = this.dataset.product;
        var action = this.checked ? 'select' : 'unselect';
        updateUserOrder(productId, action);

    });
});

// Hàm gửi yêu cầu xóa các sản phẩm được chọn
deleteBtn.addEventListener('click', function () {
    var selectedProducts = [];
    itemCheckboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            selectedProducts.push(checkbox.dataset.product);
        }
    });

    if (selectedProducts.length === 0) {
        alert("Vui lòng chọn ít nhất một sản phẩm để xóa.");
        return;
    }

    deleteSelectedItems(selectedProducts);
});

// Hàm gửi yêu cầu xóa các sản phẩm
function deleteSelectedItems(productIds) {
    var url = '/delete_selected_items/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productIds': productIds }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 'success') {
                location.reload(); // Tải lại trang để cập nhật
            } else {
                alert("Có lỗi xảy ra khi xóa sản phẩm.");
            }
        });
}