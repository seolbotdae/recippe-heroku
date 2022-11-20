<template>
  <v-container>
    <v-layout>
      <!-- 바깥쪽 살구색 배경 -->
      <v-row justify="center">
        <v-col cols="8"> 
          <v-card color="#f5efe6" height="800">
            <v-card color='#f5efe6' height="100" flat></v-card>
            <!-- 안쪽 하얀 배경 -->
            <v-row justify="center">
              <v-col xl12 md10 cols="4" align-content="center">
                <v-card color='#fefefe' height="600" rounded="xl">
          
                  <v-card-title class="justify-center">닉네임 변경</v-card-title>
                  <v-card-title class="pl-15">현재 닉네임</v-card-title>

                  <v-card-title class="justify-center pb-15">...</v-card-title>
                  <v-card-title class="pt-15 pl-15">새로운 닉네임</v-card-title>
                  
                  <v-col offset="2" cols="8">
                    <v-text-field filled label="새 닉네임" placeholder="새로운 닉네임 입력." class="pb-10"></v-text-field>
                  </v-col>

          

                  <v-row justify="center">
                    
                    <v-card-actions>
                      <v-btn outlined width="120">취소</v-btn>
                    </v-card-actions>

                    <v-card-actions>
                      <v-btn outlined width="120">확인</v-btn>
                    </v-card-actions>
                  

                  </v-row>

                  

                </v-card>
              </v-col>
            </v-row>
            

  
          </v-card>
        </v-col>
      </v-row>
    </v-layout>
  </v-container>
</template>