import { useEffect, useState } from 'react';
import ReportList from './reportList/ReportList';
import styles from './Reports.module.css'
import { PetReport } from '../../api/types';
import ServiceApi from '../../api/serviceAPI';

const Reports = () => {

    const [reports, setReports] = useState<PetReport[]>([])
    const [reportsCount, setReportsCount] = useState<number>(0);

    const fetching = async () => {
        const data = await ServiceApi.getReports();
        const total_count = await ServiceApi.getReportCount();
        setReportsCount(total_count.data.reports_count)
        setReports(data.data) 
    }

    useEffect(() => {
        fetching();
    }, [])

    return (
        <div className={styles.wrapper}>
            <h1 className={styles.title}>Объявления</h1>
            <p className={styles.count}>Общее количество объявлений: {reportsCount}</p>
            <ReportList reports={reports} setReports={setReports}/>
        </div>
    );
}
 
export default Reports;