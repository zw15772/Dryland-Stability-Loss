from __Global__ import *

class multiregression:
    def __init__(self):
        self.model_list = [

                           'composite_LAI_median']
    def run(self):
        self.statistic_corr_boxplot()

    def statistic_corr_boxplot(self):


        # === 1. read ===
        dff = result_root + rf'\Upload_Data\Figure4\1mm_new\\Obs.df'
        df = T.load_df(dff)
        df = self.df_clean(df)
        print(len(df))



        # === 2. variable ===
        variable_list = [
            'sensitivity',
            'Precip_sum_detrend_CV',
            'CV_daily_rainfall_average',
        ]

        label_dic = {
            'sensitivity': r'$\gamma$',
            'Precip_sum_detrend_CV': r'$CV_{inter}$',
            'CV_daily_rainfall_average': r'$CV_{intra}$',
        }



        for model in self.model_list:


            result_dic = {}

            # print(len(df));exit()
            for variable in variable_list:
                new_variable = f'{model}_{variable}_sig'
                if new_variable not in df.columns:
                    continue

                vals = np.array(df[new_variable].tolist(), dtype=float)
                vals[(vals > 99) | (vals < -99)] = np.nan
                vals = vals[~np.isnan(vals)]
                print(f'{variable}', len(vals))

                #     plt.hist(vals, bins=30)
                #     plt.axvline(np.mean(vals), color='g', label='Mean')
                #     plt.axvline(np.median(vals), color='r', label='Median')
                #     plt.legend()
                #     plt.show()

                # vals_mean=np.nanmean(vals)
                # print(vals_mean)
                result_dic[new_variable] = vals

            # === 5. organize data based on variable list order  ===
            data_list = []
            x_labels = []

            for var in variable_list:
                key = f'{model}_{var}_sig'
                if key in result_dic:
                    data_list.append(result_dic[key])
                    x_labels.append(label_dic[var])

                    # color
            color_list = ['#a577ad', 'yellowgreen', 'Pink', '#f599a1']
            dark_colors = ['#774685', 'Olive', 'Salmon', '#c3646f']  # 可以改为你自定义的 darken_color 函数

            # plot
            fig, ax = plt.subplots(figsize=(4, 3))

            box = ax.boxplot(
                data_list,
                patch_artist=True,
                widths=0.4,
                showfliers=False,

                showmeans=False,

            )

            # customize color

            for i, patch in enumerate(box['boxes']):
                face_color = color_list[i]
                edge_color = dark_colors[i]


                patch.set_facecolor(face_color)
                patch.set_edgecolor(edge_color)
                patch.set_linewidth(1.5)

                # median
                box['medians'][i].set_color(edge_color)
                box['medians'][i].set_linewidth(1.8)

                # （whisker）
                box['whiskers'][2 * i].set_color(edge_color)
                box['whiskers'][2 * i + 1].set_color(edge_color)
                box['whiskers'][2 * i].set_linewidth(1.2)
                box['whiskers'][2 * i + 1].set_linewidth(1.2)

                # （caps）
                box['caps'][2 * i].set_color(edge_color)
                box['caps'][2 * i + 1].set_color(edge_color)
                box['caps'][2 * i].set_linewidth(1.2)
                box['caps'][2 * i + 1].set_linewidth(1.2)

            #

            plt.xticks(range(1, len(x_labels) + 1), x_labels, fontsize=10)
            plt.xlabel('')
            plt.ylabel('Partial correlation', fontsize=10)

            plt.axhline(0, color='gray', linestyle='--')
            # plt.tight_layout()
            # plt.show()

            outdir = result_root + rf'\FIGURE\SI\\'
            Tools().mk_dir(outdir, force=True)
            plt.show()

            # outf=join(outdir,f'{model}_partial_correlation_boxplot_3mm.pdf')
            # plt.savefig(outf,bbox_inches='tight',dpi=300
            #
            # )
            # plt.close()


    def df_clean(self, df):
        T.print_head_n(df)
        # df = df.dropna(subset=[self.y_variable])
        # T.print_head_n(df)
        # exit()
        df = df[df['row'] > 60]
        df = df[df['Aridity'] < 0.65]
        df = df[df['LC_max'] < 10]
        df = df[df['MODIS_LUCC'] != 12]

        df = df[df['landcover_classfication'] != 'Cropland']

        return df

def main():
    multiregression().run()



    pass

if __name__ == '__main__':
    main()