<h1>Inventory Database</h1>
<h2>Inventory</h2>
<h3>inventory table</h3>
In this table, you can add the diferents products in the inventory.
<ul>
    <li><b>id</b></li>
        Autoincrement.
    <li><b>name</b></li>
        A string with the name of the product.
    <li><b>category</b></li>
        <i>FK of category table.</i><br>
        The category of the product. Can be 'tool' for special functions.
    <li><b>description</b></li>
        A string with the description of the product.
    <li><b>brand</b></li>
        A string with the brand of the product.
    <li><b>model</b></li>
        A string with the model of the product.
    <li><b>quantity</b></li>
        A integer that represent the quantity of the product.
</ul>
<h3>inventory_detail table</h3>
In this table, you can get into all the movements of the products in the inventory. You need to specify if it's input or output.
<ul>
    <li><b>id</b></li>
        Autoincrement.
    <li><b>date</b></li>
        The date.
    <li><b>type</b></li>
        Can be only 'input' or 'output'.
    <li><b>product_id</b></li>
        <i>FK of inventory table.</i><br>
        The product that you want to update.
    <li><b>quantity</b></li>
        Quantity of products.
    <li><b>comment</b></li>
        A free string to describe the movement.
    <li><b>origin</b></li>
        Can be only 'maintenance' or 'requisition'.
    <li><b>origin_id</b></li>
        It's the id of the score in the respective origin table.
</ul>

<h2>Requisitions</h2>
<h3>requisitions table</h3>
In this table, you can get into the requisitions.
<ul>
    <li><b>id</b></li>
    <li><b>date</b></li>
    <li><b>status</b></li>
    <li><b>description</b></li>
</ul> 

<h3>requisitions_detail table</h3>
In this table, the software will save the details of each requisitions.
<ul>
    <li><b>id</b></li>
    <li><b>requisition_id</b></li>
    <li><b>product_id</b></li>
    <li><b>quantity</b></li>
    <li><b>comment</b></li>
    <li><b>status</b></li>

</ul> 