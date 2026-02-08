from __Global__ import *

class plot_CV_trend_among_models2:
    def __init__(self):
        pass
    def run(self):
        self.plot_CV_trend_among_models2()


    def plot_CV_trend_among_models2(self):  ##here not calculating mean in program

        color_list = ['black', 'black', 'black', 'black', '#E7483D', '#a1a9d0',
                      '#f0988c', '#b883d3', '#ffff33', '#c4a5de',
                      '#984ea3', 'yellow',
                      '#9e9e9e', '#cfeaf1', '#f6cae5',
                      '#98cccb', '#5867AF', '#e66d50', ]
        ## I want use set 3 color

        mark_size_list = [200] * 1 + [50] * 3 + [200] * 1 + [50] * 13

        dff = result_root + rf'\Upload_Data\Figure3\Trends_CV\\Trends_CV_area_weighted.df'
        df = T.load_df(dff)
        df = self.df_clean(df)
        T.print_head_n(df)
        print(df.columns.tolist())
        ## print column names
        # print(df.columns)
        # exit()
        marker_list = ['^', 's', 'P', 'X', 'D'] * 4

        variables_list = ['composite_LAI_mean', 'LAI4g', 'GLOBMAP_LAI',
                          'SNU_LAI',
                          'TRENDY_ensemble_median',
                          'CABLE-POP_S2_lai', 'CLASSIC_S2_lai',
                          'CLM5', 'DLEM_S2_lai', 'IBIS_S2_lai', 'ISAM_S2_lai',
                          'ISBA-CTRIP_S2_lai', 'JSBACH_S2_lai',
                          'JULES_S2_lai', 'LPJ-GUESS_S2_lai', 'LPX-Bern_S2_lai',
                          'ORCHIDEE_S2_lai',

                          'YIBs_S2_Monthly_lai']
        vals_trend_list = []
        vals_CV_list = []
        err_trend_list = []
        err_CV_list = []

        for variable in variables_list:
            vals_trend = df[f'{variable}_relative_change_trend'].values
            vals_CV = df[f'{variable}_detrend_CV_trend'].values
            valid = (
                    np.isfinite(vals_CV) &
                    (vals_CV > -999) & (vals_CV < 999)
            )
            weight = np.array(df['area_weight'].tolist(), dtype=float)
            weighted_mean_values_CV = (
                    np.sum(vals_CV[valid] * weight[valid])
                    / np.sum(weight[valid])
            )
            valid_trend = (
                    np.isfinite(vals_trend) &
                    (vals_trend > -999) & (vals_trend < 999)
            )

            weighted_mean_values_trend = (
                    np.sum(vals_trend[valid_trend] * weight[valid_trend])
                    / np.sum(weight[valid_trend])
            )

            vals_trend_list.append(weighted_mean_values_trend)
            vals_CV_list.append(weighted_mean_values_CV)
        # print(vals_trend_list)
        # print(vals_CV_list);exit()
        ### ranking vals_trend_list
        vals_trend_list = np.array(vals_trend_list)
        vals_trend_list_sort = np.sort(vals_trend_list)

        print(vals_trend_list_sort)

        vals_CV_list = np.array(vals_CV_list)
        vals_CV_list_sort = np.sort(vals_CV_list)

        print(vals_CV_list_sort);
        # exit()

        # exit()

        n = len(variables_list)
        mark_size_list = mark_size_list[:n]
        color_list = color_list[:n]
        marker_list = marker_list[:n]

        # plt.scatter(vals_CV_list,vals_trend_list,marker=marker_list,color=color_list[0],s=100)
        # plt.show()
        ##plot error bar
        # plt.figure(figsize=(self.map_width, self.map_height))

        plt.figure(figsize=(13 * centimeter_factor, 10 * centimeter_factor))

        # self.map_width = 13 * centimeter_factor
        # self.map_height = 8.2 * centimeter_factor

        err_trend_list = np.array(err_trend_list)
        err_CV_list = np.array(err_CV_list)
        for i, (x, y, marker, color, var, mark_size) in enumerate(
                zip(vals_trend_list, vals_CV_list, marker_list, color_list, variables_list, mark_size_list)):
            plt.scatter(y, x, marker=marker, color=color_list[i], label=var, s=mark_size, edgecolors='black', )
            # plt.errorbar(y, x, xerr=err_trend_list[i], yerr=err_CV_list[i], fmt='none', color='grey', capsize=2, capthick=0.3,alpha=1)

            ##markerborderwidth=1

            plt.ylabel('Trends in LAI (%/yr)', fontsize=12)
            plt.xlabel('Trends in CVLAI (%/yr)', fontsize=12)
            plt.ylim(-0.3, .9)
            plt.xlim(-0.2, 0.5)
            plt.xticks(fontsize=12)
            ## xticks gap 0.05
            plt.yticks(np.arange(-0.2, .9, 0.2), fontsize=12)
            plt.yticks(fontsize=12)
            # plt.legend()
        ## save imagine
        # plt.axhline(y=0.0, color='k', linestyle='--', linewidth=1)
        # plt.axvline(x=0.0, color='k', linestyle='--', linewidth=1)
        # plt.savefig(result_root + rf'\FIGURE\\weighted_area\\obs_TRENDY_CV_trends_mean.pdf', bbox_inches='tight')

        #
        plt.show()

    pass

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
    plot_CV_trend_among_models2().run()

    pass

if __name__ == '__main__':
    main()