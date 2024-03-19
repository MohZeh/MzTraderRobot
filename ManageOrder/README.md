# Class Documentation: SpotOrderManager

#### 1. General Explanation:
The `SpotOrderManager` class is designed to manage orders in trading markets. This class utilizes APIs related to orders to provide functionalities such as placing orders, deleting orders, and retrieving order information.

#### 2. Methods and Usage:

- **`__init__(self, api_key)`**:  
  - **Description**: Initializes an instance of the `SpotOrderManager` class with the specified API key.
  - **Parameters**:
    - `api_key`: The API key for accessing Wallex services.
  - **Example**:
    ```python
    API_KEY = "X-API-Key"
    order_manage_instance = SpotOrderManager(api_key=API_KEY)
    ```

- **`get_open_orders_id(self)`**:  
  - **Description**: Retrieves the IDs of open orders.
  - **Returns**: A list of open order IDs.
  - **Example**:
    ```python
    orders_id = order_manage_instance.get_open_orders_id()
    ```

- **`set_order_params(self, order_params)`**:  
  - **Description**: Sets the necessary parameters for placing an order.
  - **Parameters**:
    - `order_params`: A dictionary containing order information including symbol, order type, side, price, and quantity.
  - **Example**:
    ```python
    order_params = {
        "symbol": "SHIBTMN",
        "type_order": "LIMIT",
        "side": "BUY",
        "price": 0.5000,
        "quantity": "400000",
        "specific_order_id": "MohZeh-SHIBTMN"
    }
    ```

- **`order_manage(self, order_params)`**:  
  - **Description**: Manages orders based on the given parameters.
  - **Parameters**:
    - `order_params`: Parameters related to the order.
  - **Returns**: The status of placing the order (success or failure).
  - **Example**:
    ```python
    status_order = order_manage_instance.order_manage(order_params=order_params)
    ```

#### 3. Examples:

1. Retrieving open order IDs and their information:
    ```python
    orders_id = order_manage_instance.get_open_orders_id()
    for i in orders_id:
        print("Order ID:", i)
        order_manage_instance.get_order_result(order_id=i)
    ```

2. Placing an order:
    ```python
    status_order = order_manage_instance.order_manage(order_params=order_params)
    print("Order placement status:", status_order)
    ```

#### 4. Conclusion:
The `SpotOrderManager` class provides users with the ability to manage orders in trading markets. By utilizing the methods of this class and setting the required parameters, users can confidently place their orders with assurance of correctness and executability.

# راهنما و مستندات کلاس SpotOrderManager

#### ۱. توضیحات کلی:
کلاس `SpotOrderManager` برای مدیریت سفارشات در بازارهای معاملاتی طراحی شده است. این کلاس از API‌های مربوط به سفارشات استفاده می‌کند تا امکاناتی مانند قراردادن سفارشات، حذف سفارشات و بازیابی اطلاعات سفارشات را فراهم کند.

#### ۲. متدها و استفاده:

- **`__init__(self, api_key)`**:  
  - **توضیحات**: یک نمونه از کلاس `SpotOrderManager` را با استفاده از کلید API معین شده ایجاد می‌کند.
  - **پارامترها**:
    - `api_key`: کلید API برای دسترسی به سرویس‌های والکس.
  - **مثال**:
    ```python
    API_KEY = "X-API-Key"
    order_manage_instance = SpotOrderManager(api_key=API_KEY)
    ```

- **`get_open_orders_id(self)`**:  
  - **توضیحات**: شناسه‌های سفارشات باز را بازیابی می‌کند.
  - **بازگشت**: لیست شناسه‌های سفارشات باز.
  - **مثال**:
    ```python
    orders_id = order_manage_instance.get_open_orders_id()
    ```

- **`set_order_params(self, order_params)`**:  
  - **توضیحات**: پارامترهای لازم برای قراردادن سفارش را تنظیم می‌کند.
  - **پارامترها**:
    - `order_params`: یک دیکشنری حاوی اطلاعات سفارش از جمله نماد، نوع سفارش، جنسیت، قیمت و تعداد.
  - **مثال**:
    ```python
    order_params = {
        "symbol": "SHIBTMN",
        "type_order": "LIMIT",
        "side": "BUY",
        "price": 0.5000,
        "quantity": "400000",
        "specific_order_id": "MohZeh-SHIBTMN"
    }
    ```

- **`order_manage(self, order_params)`**:  
  - **توضیحات**: مدیریت سفارشات بر اساس پارامترهای داده شده، اعمال می‌شود.
  - **پارامترها**:
    - `order_params`: پارامترهای مربوط به سفارش.
  - **بازگشت**: وضعیت قراردادن سفارش (موفقیت یا شکست).
  - **مثال**:
    ```python
    status_order = order_manage_instance.order_manage(order_params=order_params)
    ```

#### ۳. مثال‌ها:

۱. بازیابی شناسه‌های سفارشات باز و اطلاعات آن‌ها:

```python
    orders_id = order_manage_instance.get_open_orders_id()
    for i in orders_id:
        print("Order ID:", i)
        order_manage_instance.get_order_result(order_id=i)
```

۲. قراردادن یک سفارش:

```python
    status_order = order_manage_instance.order_manage(order_params=order_params)
    print("Order placement status:", status_order)
```

#### ۴. نتیجه‌گیری:
کلاس `SpotOrderManager` به کاربران امکان مدیریت سفارشات در بازارهای معاملاتی را ارائه می‌دهد. با استفاده از متدهای این کلاس و با تنظیم پارامترهای مورد نیاز، کاربران می‌توانند سفارشات خود را با اطمینان از صحت و قابلیت اجرا قرار دهند.
