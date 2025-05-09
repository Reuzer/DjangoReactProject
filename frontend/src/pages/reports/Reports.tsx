import { useEffect, useState } from 'react';
import ReportList from './reportList/ReportList';
import styles from './Reports.module.css'
import { PetReport } from '../../api/types';
import ServiceApi from '../../api/serviceAPI';

const Reports = () => {

    const [reports, setReports] = useState<PetReport[]>([])

    const fetching = async () => {
        const data = await ServiceApi.getReports();
        setReports(data.data) 
    }

    useEffect(() => {
        fetching();
    }, [])

    return (
        <div className={styles.wrapper}>
            <h1 className={styles.title}>Объявления</h1>
            <ReportList reports={reports}/>
        </div>
    );
}
 
export default Reports;