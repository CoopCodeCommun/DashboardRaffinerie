<template>
  <div class="col case">
    <div class="container-fluid">
      <div class="row d-flex">
        <nav class="p-0 vert sidebar case">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item" v-for="(menuItem, index) in menuItems" :key="index">
                <button class="btn m-2 rounded b-0 menu_lateral text-start">
                  <i :class="menuItem.icon"></i> {{ menuItem.text }}
                </button>
              </li>
            </ul>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['menuItems']
};
</script>
