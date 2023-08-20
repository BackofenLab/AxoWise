<template>
    <div id="pathways-list">
        <img id="pathway-search" src="@/assets/pathwaybar/pathway-button.png">
        <img id="pathway-filter" src="@/assets/pathwaybar/pathway-button-2.png">
        <div class="bookmark-button"></div>
        <div class="visualize-button"></div>
        <div class="export-button"></div>
        <div class="list-section"></div>

    </div>
</template>

<script>

export default {
    name: 'PathwayList',
    
}
</script>


<style>
    #pathways-list {
        width: 32.83%;
        height: 96.92%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
        margin-left: 0.28%;
        border-radius: 10px;
        z-index: 999;
    }

    #pathway-search {
        width: 37.54%;
        height: 11.16%;
        position: absolute;
    }

    #pathway-filter {
        width: 20.54%;
        left: 35.7%;
        height: 11.16%;
        position: absolute;
    }
    .list-section {
        width: 100%;
        height: 87.65%;
        top: 12.35%;
        border-radius: 10px;
        background: #0A0A1A;
        position: absolute;
    }
    .bookmark-button {
        width: 7.51%;
        height: 11.16%;
        left: 57.35%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
    }
    .visualize-button {
        width: 17.24%;
        height: 11.16%;
        left: 65.86%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
    }
    .export-button {
        width: 15.8%;
        height: 11.16%;
        left: 84.1%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
    }
</style>