document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form");
    const formButton = document.getElementById("form-button");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Ngăn gửi form mặc định

        // Lấy dữ liệu từ form
        const reciName = form.querySelector('input[name="reci-name"]').value;
        const reciPhone = form.querySelector('input[name="email"]').value;
        const address = form.querySelector('input[name="address"]').value;
        const city = form.querySelector('input[name="city"]').value;
        const province = form.querySelector('input[name="province"]').value;

        // Gửi dữ liệu đến server
        const url = "/shipping/"; // Đường dẫn API bạn định nghĩa

        const payload = {
            reci_name: reciName,
            reci_phone: reciPhone,
            address: address,
            city: city,
            province: province,
        };

        formButton.disabled = true; // Khóa nút thanh toán trong khi xử lý

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(payload),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Lỗi khi xử lý thanh toán");
                }
            })
            .then((data) => {
                alert("Thanh toán thành công! Đơn hàng mới đã được tạo.");
                window.location.href = "/cart/"; // Chuyển hướng tới trang danh sách đơn hàng
            })
            .catch((error) => {
                alert(error.message);
                formButton.disabled = false; // Mở khóa nút thanh toán nếu lỗi
            });
    });
});
