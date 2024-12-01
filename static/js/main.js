async function cartUpdate(e) {
    const { data } = await axios(e.dataset.url)
    const { message, items_count } = data
    notyf.success({
    message,
    dismissible: true,
    icon: false
    })
    document.getElementById('cart-items-count').innerHTML = items_count

}

async function cartRemove(e) {
    await axios(e.dataset.url)
    location.reload()
}

function switchPaymentMethod(type, content) {
   const stripeCard = document.getElementById('stripe-card');
       stripeCard.style.display = 'block'

}

//async function cartUpdate(e) {
//    try {
//        const { data } = await axios(e.dataset.url);
//        const { message, items_count } = data;
//
//        notyf.success({
//            message,
//            dismissible: true,
//            icon: false
//        });
//
//        document.getElementById('cart-items-count').innerHTML = items_count;
//    } catch (error) {
//        // التعامل مع الأخطاء
//        console.error('Error adding item to cart:', error);
//
//        // إظهار رسالة خطأ للمستخدم
//        notyf.error({
//            message: 'There was an error adding the item to your cart. Please try again.',
//            dismissible: true,
//            icon: false
//        });
//    }
//}