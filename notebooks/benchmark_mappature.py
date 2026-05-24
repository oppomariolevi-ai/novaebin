"""
Benchmark di mappature binarie per l'ALU Novae.
Dimostra il Capitolo 6, Sezione 6.3 del Principia Novae Mathematicae v1.3.
"""

# Scrittura e compilazione del benchmark C
codice_c = '''
#include <stdio.h>
#include <time.h>

#define N 100000000

static int V_Lineare[32] = {-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10};
static int V_Gray[32] = {[0]=-10,[1]=-9,[3]=-8,[2]=-7,[6]=-6,[7]=-5,[5]=-4,[4]=-3,[12]=-2,[13]=-1,[15]=0,[14]=1,[10]=2,[11]=3,[9]=4,[8]=5,[24]=6,[25]=7,[27]=8,[26]=9,[30]=10};
static int V_Complementare[32] = {[21]=-10,[22]=-9,[23]=-8,[24]=-7,[25]=-6,[26]=-5,[27]=-4,[28]=-3,[29]=-2,[30]=-1,[0]=0,[1]=1,[2]=2,[3]=3,[4]=4,[5]=5,[6]=6,[7]=7,[8]=8,[9]=9,[10]=10};

int main() {
    clock_t start, end;
    volatile int sum;

    sum = 0; start = clock();
    for (int i = 0; i < N; i++) {
        int va = V_Lineare[i % 21];
        int vb = V_Lineare[(i*3+7) % 21];
        int vsum = va + vb;
        if (vsum > 10) vsum -= 21;
        else if (vsum < -10) vsum += 21;
        sum += vsum;
    }
    end = clock();
    printf("Tempo Lineare: %.6f s\\n", ((double)(end - start)) / CLOCKS_PER_SEC);

    sum = 0; start = clock();
    for (int i = 0; i < N; i++) {
        int va = V_Gray[i % 21];
        int vb = V_Gray[(i*3+7) % 21];
        int vsum = va + vb;
        if (vsum > 10) vsum -= 21;
        else if (vsum < -10) vsum += 21;
        sum += vsum;
    }
    end = clock();
    printf("Tempo Gray: %.6f s\\n", ((double)(end - start)) / CLOCKS_PER_SEC);

    sum = 0; start = clock();
    for (int i = 0; i < N; i++) {
        int va = V_Complementare[i % 21];
        int vb = V_Complementare[(i*3+7) % 21];
        int vsum = va + vb;
        if (vsum > 10) vsum -= 21;
        else if (vsum < -10) vsum += 21;
        sum += vsum;
    }
    end = clock();
    printf("Tempo Complementare: %.6f s\\n", ((double)(end - start)) / CLOCKS_PER_SEC);

    return 0;
}
'''

with open('bench_map.c', 'w') as f:
    f.write(codice_c)

import subprocess
subprocess.run(['gcc', '-O2', '-o', 'bench_map', 'bench_map.c'])

result = subprocess.run(['./bench_map'], capture_output=True, text=True)
print(result.stdout)
